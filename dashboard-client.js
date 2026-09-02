/**
 * Real-Time Dashboard WebSocket Client
 *
 * This is a vanilla JavaScript client for consuming real-time updates
 * from the BBQ Restaurant AI BI platform's WebSocket endpoints.
 *
 * Can be integrated into React, Vue, Svelte, or plain HTML dashboard.
 *
 * Usage:
 *   const client = new DashboardClient('ws://localhost:8000');
 *   client.connect({branch_id: 1, user_id: 'user123'});
 *   client.on('anomaly_detected', (alert) => console.log(alert));
 */

class DashboardClient {
  /**
   * Create a new dashboard WebSocket client.
   *
   * @param {string} wsUrl - WebSocket server URL (e.g., 'ws://localhost:8000')
   */
  constructor(wsUrl = 'ws://localhost:8000') {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.clientId = null;
    this.isConnected = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 10;
    this.reconnectDelay = 3000; // 3 seconds

    // Event handlers
    this.handlers = {};

    // Message queues
    this.messageQueue = [];
    this.isProcessing = false;
  }

  /**
   * Connect to the WebSocket endpoint.
   *
   * @param {Object} options - Connection options
   * @param {number} options.branch_id - Optional branch ID filter
   * @param {string} options.user_id - Optional user identifier
   * @param {string} options.endpoint - Which endpoint: 'dashboard' (default) or 'alerts'
   */
  connect(options = {}) {
    const {
      branch_id = null,
      user_id = null,
      endpoint = 'dashboard'
    } = options;

    // Build WebSocket URL with query parameters
    const params = new URLSearchParams();
    if (branch_id !== null) params.append('branch_id', branch_id);
    if (user_id !== null) params.append('user_id', user_id);

    const url = `${this.wsUrl}/ws/${endpoint}${params.toString() ? '?' + params.toString() : ''}`;

    console.log(`[Dashboard Client] Connecting to: ${url}`);

    try {
      this.ws = new WebSocket(url);

      this.ws.onopen = () => this._onOpen();
      this.ws.onmessage = (event) => this._onMessage(event);
      this.ws.onerror = (event) => this._onError(event);
      this.ws.onclose = () => this._onClose();
    } catch (error) {
      console.error('[Dashboard Client] Connection error:', error);
      this._scheduleReconnect();
    }
  }

  /**
   * Disconnect from the WebSocket.
   */
  disconnect() {
    if (this.ws) {
      this.isConnected = false;
      this.ws.close();
      this.ws = null;
      console.log('[Dashboard Client] Disconnected');
    }
  }

  /**
   * Register a handler for a message type.
   *
   * @param {string} eventType - Message type (e.g., 'anomaly_detected', 'kpi_update')
   * @param {Function} handler - Callback function(message)
   */
  on(eventType, handler) {
    if (!this.handlers[eventType]) {
      this.handlers[eventType] = [];
    }
    this.handlers[eventType].push(handler);
    console.log(`[Dashboard Client] Registered handler for: ${eventType}`);
  }

  /**
   * Unregister a handler.
   *
   * @param {string} eventType - Message type
   * @param {Function} handler - Handler to remove
   */
  off(eventType, handler) {
    if (this.handlers[eventType]) {
      this.handlers[eventType] = this.handlers[eventType].filter(h => h !== handler);
    }
  }

  /**
   * Send a message to the server (for future client->server commands).
   *
   * @param {Object} message - Message object
   */
  send(message) {
    if (this.isConnected && this.ws) {
      try {
        this.ws.send(JSON.stringify(message));
      } catch (error) {
        console.error('[Dashboard Client] Send error:', error);
      }
    } else {
      console.warn('[Dashboard Client] Not connected, queuing message');
      this.messageQueue.push(message);
    }
  }

  /**
   * Subscribe to specific event types (for alerts endpoint).
   *
   * @param {Array<string>} eventTypes - Event types to subscribe to
   */
  subscribe(eventTypes) {
    this.send({
      type: 'subscribe',
      event_types: eventTypes
    });
  }

  /**
   * Unsubscribe from event types.
   *
   * @param {Array<string>} eventTypes - Event types to unsubscribe from
   */
  unsubscribe(eventTypes) {
    this.send({
      type: 'unsubscribe',
      event_types: eventTypes
    });
  }

  // ========================================================================
  // Private Methods
  // ========================================================================

  _onOpen() {
    console.log('[Dashboard Client] Connected');
    this.isConnected = true;
    this.reconnectAttempts = 0;

    // Send queued messages
    while (this.messageQueue.length > 0) {
      this.send(this.messageQueue.shift());
    }

    this._emit('connected', { clientId: this.clientId });
  }

  _onMessage(event) {
    try {
      const message = JSON.parse(event.data);
      this._processMessage(message);
    } catch (error) {
      console.error('[Dashboard Client] Parse error:', error);
    }
  }

  _processMessage(message) {
    const { type, ...data } = message;

    // Handle connection ack specially
    if (type === 'connection_ack') {
      this.clientId = data.client_id;
      console.log(`[Dashboard Client] Connected with ID: ${this.clientId}`);
    }

    // Emit to handlers
    this._emit(type, data);

    // Also emit 'all_messages' for debugging
    this._emit('all_messages', message);
  }

  _emit(eventType, data) {
    if (this.handlers[eventType]) {
      this.handlers[eventType].forEach(handler => {
        try {
          handler(data);
        } catch (error) {
          console.error(`[Dashboard Client] Handler error for ${eventType}:`, error);
        }
      });
    }
  }

  _onError(event) {
    console.error('[Dashboard Client] WebSocket error:', event);
    this._emit('error', event);
  }

  _onClose() {
    console.log('[Dashboard Client] Connection closed');
    this.isConnected = false;
    this._emit('disconnected', {});

    // Attempt to reconnect
    this._scheduleReconnect();
  }

  _scheduleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * this.reconnectAttempts;
      console.log(`[Dashboard Client] Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

      setTimeout(() => this.connect(), delay);
    } else {
      console.error('[Dashboard Client] Max reconnection attempts reached');
      this._emit('reconnect_failed', {});
    }
  }
}

// ============================================================================
// Example Usage
// ============================================================================

if (typeof module !== 'undefined' && module.exports) {
  module.exports = DashboardClient;
}

// HTML Example:
/*
<!DOCTYPE html>
<html>
<head>
  <title>BBQ Restaurant Real-Time Dashboard</title>
  <style>
    body { font-family: Arial; margin: 20px; }
    .alert { padding: 10px; margin: 10px 0; border-radius: 5px; }
    .alert.low { background: #d4edda; border: 1px solid #c3e6cb; }
    .alert.medium { background: #fff3cd; border: 1px solid #ffeeba; }
    .alert.high { background: #f8d7da; border: 1px solid #f5c6cb; }
    .alert.critical { background: #f5c6cb; border: 1px solid #721c24; }
    .kpi { display: inline-block; margin: 10px; padding: 15px; border: 1px solid #ddd; }
    #status { padding: 10px; background: #e9ecef; margin: 10px 0; }
  </style>
</head>
<body>
  <h1>BBQ Restaurant Real-Time Dashboard</h1>

  <div id="status">Status: <strong>Connecting...</strong></div>

  <h2>Key Performance Indicators</h2>
  <div id="kpis"></div>

  <h2>Real-Time Alerts</h2>
  <div id="alerts"></div>

  <h2>Recent Messages</h2>
  <div id="messages" style="max-height: 300px; overflow-y: auto; border: 1px solid #ddd; padding: 10px;"></div>

  <script src="dashboard-client.js"></script>
  <script>
    // Initialize client
    const client = new DashboardClient('ws://localhost:8000');

    // Track state
    const state = {
      alerts: [],
      kpis: {},
      messageCount: 0
    };

    // ===== Connection Events =====
    client.on('connected', (data) => {
      updateStatus('Connected', 'healthy');
      console.log('Dashboard connected:', data);
    });

    client.on('disconnected', () => {
      updateStatus('Disconnected', 'offline');
    });

    client.on('error', (error) => {
      updateStatus('Error', 'error');
    });

    // ===== Anomaly Alerts =====
    client.on('anomaly_detected', (alert) => {
      console.log('Anomaly alert:', alert);

      const alertEl = document.createElement('div');
      alertEl.className = `alert ${alert.severity}`;
      alertEl.innerHTML = `
        <strong>${alert.metric.toUpperCase()}</strong>: ${alert.description}
        <br/>Deviation: ${alert.deviation_percent.toFixed(1)}%
        <br/><small>${new Date(alert.timestamp).toLocaleTimeString()}</small>
      `;

      const alertsDiv = document.getElementById('alerts');
      alertsDiv.insertBefore(alertEl, alertsDiv.firstChild);

      // Keep only last 10 alerts
      while (alertsDiv.children.length > 10) {
        alertsDiv.removeChild(alertsDiv.lastChild);
      }
    });

    // ===== Forecast Alerts =====
    client.on('forecast_alert', (forecast) => {
      console.log('Forecast alert:', forecast);

      const alertEl = document.createElement('div');
      alertEl.className = 'alert medium';
      alertEl.innerHTML = `
        <strong>Forecast: ${forecast.metric}</strong>
        <br/>Trend: ${forecast.trend} | Confidence: ${(forecast.confidence * 100).toFixed(0)}%
        <br/>Predicted: ${forecast.predicted_value.toLocaleString()}
        <br/>${forecast.recommendation || ''}
        <br/><small>${new Date(forecast.timestamp).toLocaleTimeString()}</small>
      `;

      const alertsDiv = document.getElementById('alerts');
      alertsDiv.insertBefore(alertEl, alertsDiv.firstChild);
    });

    // ===== KPI Updates =====
    client.on('kpi_update', (kpis) => {
      console.log('KPI update:', kpis);

      const kpisDiv = document.getElementById('kpis');
      kpisDiv.innerHTML = '';

      Object.entries(kpis.kpis || {}).forEach(([key, value]) => {
        const kpiEl = document.createElement('div');
        kpiEl.className = 'kpi';
        kpiEl.innerHTML = `
          <strong>${key}</strong><br/>
          ${typeof value === 'number' ? value.toLocaleString() : value}
        `;
        kpisDiv.appendChild(kpiEl);
      });
    });

    // ===== Single Metric Updates =====
    client.on('metrics_update', (metric) => {
      console.log('Metric update:', metric);
      updateMessage(`${metric.metric_name}: ${metric.value}`);
    });

    // ===== All Messages (for debugging) =====
    client.on('all_messages', (message) => {
      state.messageCount++;
      updateMessage(`[${message.type}] ${JSON.stringify(message).substring(0, 100)}...`);
    });

    // ===== Helper Functions =====
    function updateStatus(text, status) {
      const el = document.getElementById('status');
      el.innerHTML = `Status: <strong style="color: ${status === 'healthy' ? 'green' : status === 'offline' ? 'red' : 'orange'}">${text}</strong> (${state.messageCount} messages)`;
    }

    function updateMessage(text) {
      const messagesDiv = document.getElementById('messages');
      const msgEl = document.createElement('div');
      msgEl.style.fontSize = '12px';
      msgEl.style.marginBottom = '5px';
      msgEl.innerHTML = `<code>${new Date().toLocaleTimeString()}: ${text}</code>`;
      messagesDiv.insertBefore(msgEl, messagesDiv.firstChild);

      // Keep only last 50 messages
      while (messagesDiv.children.length > 50) {
        messagesDiv.removeChild(messagesDiv.lastChild);
      }
    }

    // Connect to WebSocket
    client.connect({
      branch_id: 1,
      user_id: 'dashboard_user',
      endpoint: 'dashboard'
    });

    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
      client.disconnect();
    });
  </script>
</body>
</html>
*/
