class ThermostatCard extends HTMLElement {
    setConfig(config) {
        if (!config.entity) {
            throw new Error("You need to define an entity");
        }
        this.config = config;
        this.attachShadow({ mode: "open" });
    }

    set hass(hass) {
        const entityId = this.config.entity;
        const state = hass.states[entityId];

        if (!state) {
            this.shadowRoot.innerHTML = `<ha-card><div style="padding: 16px;">Entity not found: ${entityId}</div></ha-card>`;
            return;
        }

        const currentTemp = state.attributes.current_temperature || "N/A";
        const targetTemp = state.attributes.target_temperature || "N/A";
        const hvacMode = state.state || "off";
        const boostMode = state.attributes.boost_mode ? "Active" : "Inactive";

        this.shadowRoot.innerHTML = `
      <style>
        ha-card {
          padding: 16px;
          font-family: Arial, sans-serif;
        }
        .controls {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .status {
          margin: 8px 0;
        }
      </style>
      <ha-card>
        <h1>${state.attributes.friendly_name || "Thermostat"}</h1>
        <div class="status">
          <div>Current Temperature: <strong>${currentTemp}°C</strong></div>
          <div>Target Temperature: <strong>${targetTemp}°C</strong></div>
          <div>HVAC Mode: <strong>${hvacMode}</strong></div>
          <div>Boost Mode: <strong>${boostMode}</strong></div>
        </div>
        <div class="controls">
          <div>
            <button id="heat">Heat</button>
            <button id="cool">Cool</button>
            <button id="off">Off</button>
          </div>
          <div>
            <input type="number" id="target-temp" value="${targetTemp}" step="0.5" />
            <button id="set-temp">Set Temperature</button>
          </div>
          <div>
            <button id="boost">${boostMode === "Active" ? "Disable" : "Enable"} Boost</button>
          </div>
        </div>
      </ha-card>
    `;

        this.shadowRoot.querySelector("#heat").addEventListener("click", () => {
            hass.callService("climate", "set_hvac_mode", { entity_id: entityId, hvac_mode: "heat" });
        });
        this.shadowRoot.querySelector("#cool").addEventListener("click", () => {
            hass.callService("climate", "set_hvac_mode", { entity_id: entityId, hvac_mode: "cool" });
        });
        this.shadowRoot.querySelector("#off").addEventListener("click", () => {
            hass.callService("climate", "set_hvac_mode", { entity_id: entityId, hvac_mode: "off" });
        });
        this.shadowRoot.querySelector("#set-temp").addEventListener("click", () => {
            const targetTemp = parseFloat(this.shadowRoot.querySelector("#target-temp").value);
            hass.callService("climate", "set_temperature", { entity_id: entityId, temperature: targetTemp });
        });
        this.shadowRoot.querySelector("#boost").addEventListener("click", () => {
            const boost = boostMode !== "Active";
            hass.callService("climate", "set_preset_mode", { entity_id: entityId, preset_mode: boost ? "boost" : "none" });
        });
    }

    getCardSize() {
        return 3;
    }
}

customElements.define("thermostat-card", ThermostatCard);
