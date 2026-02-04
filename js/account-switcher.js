/**
 * Account Switcher Component for ZOE STUDIO Dashboard
 * Handles multi-client switching with localStorage persistence
 */

class AccountSwitcher {
  constructor(containerId = 'account-switcher') {
    this.containerId = containerId;
    this.clients = [];
    this.currentClient = null;
    this.isOpen = false;
  }

  /**
   * Initialize the account switcher
   */
  async init() {
    try {
      // Load clients from manifest
      this.clients = await this.loadClients();
      
      if (this.clients.length === 0) {
        console.error('No clients found in config');
        return;
      }

      // Restore last selected client or default to first
      const savedClientId = localStorage.getItem('zoestudio_current_client');
      this.currentClient = this.clients.find(c => c.id === savedClientId) || this.clients[0];
      
      // Load detailed config for current client
      await this.loadClientConfig(this.currentClient.id);
      
      // Render UI
      this.render();
      
      // Emit initial change event
      this.emitChange();
      
      console.log('Account Switcher initialized:', this.currentClient.name);
    } catch (error) {
      console.error('Failed to initialize AccountSwitcher:', error);
    }
  }

  /**
   * Load clients list from manifest
   */
  async loadClients() {
    const response = await fetch('/zoe-dashboard/config/clients.json');
    const data = await response.json();
    return data.clients.filter(c => c.status === 'active' || c.status === 'demo');
  }

  /**
   * Load detailed config for a specific client
   */
  async loadClientConfig(clientId) {
    const response = await fetch(`/zoe-dashboard/config/clients/${clientId}.json`);
    const config = await response.json();
    
    // Merge config into current client
    Object.assign(this.currentClient, config);
    
    return config;
  }

  /**
   * Select a different client
   */
  async selectClient(clientId) {
    if (clientId === this.currentClient?.id) {
      this.toggleDropdown();
      return;
    }

    // Find the client
    const client = this.clients.find(c => c.id === clientId);
    if (!client) {
      console.error('Client not found:', clientId);
      return;
    }

    // Load detailed config
    this.currentClient = client;
    await this.loadClientConfig(clientId);
    
    // Save to localStorage
    localStorage.setItem('zoestudio_current_client', clientId);
    
    // Update UI
    this.render();
    this.closeDropdown();
    
    // Emit change event
    this.emitChange();
  }

  /**
   * Emit client change event
   */
  emitChange() {
    const event = new CustomEvent('clientChanged', {
      detail: { 
        client: this.currentClient,
        clientId: this.currentClient.id
      }
    });
    window.dispatchEvent(event);
    
    console.log('Client changed to:', this.currentClient.name);
  }

  /**
   * Toggle dropdown visibility
   */
  toggleDropdown() {
    this.isOpen = !this.isOpen;
    const dropdown = document.querySelector('.account-switcher-dropdown');
    if (dropdown) {
      dropdown.classList.toggle('hidden', !this.isOpen);
    }
  }

  /**
   * Close dropdown
   */
  closeDropdown() {
    this.isOpen = false;
    const dropdown = document.querySelector('.account-switcher-dropdown');
    if (dropdown) {
      dropdown.classList.add('hidden');
    }
  }

  /**
   * Render the account switcher UI
   */
  render() {
    const container = document.getElementById(this.containerId);
    if (!container) {
      console.error('Account switcher container not found');
      return;
    }

    container.innerHTML = `
      <div class="account-switcher-wrapper relative">
        <!-- Current Account Button -->
        <button 
          class="account-switcher-button flex items-center gap-3 px-4 py-3 rounded-xl bg-surface-800 border border-zinc-700/50 hover:border-zinc-600 transition-all w-full text-left"
          onclick="accountSwitcher.toggleDropdown()"
        >
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br ${this.getGradient(this.currentClient.id)} flex items-center justify-center text-white font-bold text-sm flex-shrink-0">
            ${this.currentClient.name.charAt(0)}
          </div>
          <div class="flex-1 min-w-0">
            <p class="font-medium text-sm text-zinc-100 truncate">${this.currentClient.name}</p>
            <p class="text-xs text-zinc-500 truncate">${this.currentClient.location || 'Unknown'}</p>
          </div>
          <i class="fas fa-chevron-down text-zinc-500 text-xs"></i>
        </button>

        <!-- Dropdown Menu -->
        <div class="account-switcher-dropdown absolute top-full left-0 right-0 mt-2 bg-surface-800 border border-zinc-700/50 rounded-xl shadow-2xl z-50 hidden">
          <div class="p-2 max-h-96 overflow-y-auto">
            <!-- Client List -->
            ${this.clients.map(client => `
              <button
                class="account-switcher-item flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-surface-700 transition-all w-full text-left ${client.id === this.currentClient.id ? 'bg-brand-500/10 border border-brand-500/20' : ''}"
                onclick="accountSwitcher.selectClient('${client.id}')"
              >
                <div class="w-8 h-8 rounded-lg bg-gradient-to-br ${this.getGradient(client.id)} flex items-center justify-center text-white font-bold text-sm flex-shrink-0">
                  ${client.name.charAt(0)}
                </div>
                <div class="flex-1 min-w-0">
                  <p class="font-medium text-sm text-zinc-100 truncate">${client.name}</p>
                  <p class="text-xs text-zinc-500 truncate">${client.location || 'Unknown'}</p>
                </div>
                ${client.id === this.currentClient.id ? '<i class="fas fa-check text-brand-500 text-sm"></i>' : ''}
              </button>
            `).join('')}
            
            <!-- Add Client Button (Future) -->
            <hr class="my-2 border-zinc-700/50">
            <button class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-surface-700 transition-all w-full text-left text-zinc-400 hover:text-zinc-200">
              <div class="w-8 h-8 rounded-lg border-2 border-dashed border-zinc-600 flex items-center justify-center">
                <i class="fas fa-plus text-sm"></i>
              </div>
              <span class="text-sm font-medium">Add New Client</span>
            </button>
          </div>
        </div>
      </div>
    `;

    // Bind close on outside click
    this.bindOutsideClick();
  }

  /**
   * Get gradient colors for client avatar
   */
  getGradient(clientId) {
    const gradients = {
      'kona-coffee-2142': 'from-orange-500 to-red-500',
      'demo-client': 'from-blue-500 to-purple-500',
      'default': 'from-gray-500 to-gray-700'
    };
    return gradients[clientId] || gradients['default'];
  }

  /**
   * Bind outside click to close dropdown
   */
  bindOutsideClick() {
    document.addEventListener('click', (e) => {
      const wrapper = document.querySelector('.account-switcher-wrapper');
      if (wrapper && !wrapper.contains(e.target) && this.isOpen) {
        this.closeDropdown();
      }
    });
  }

  /**
   * Get current client data
   */
  getCurrentClient() {
    return this.currentClient;
  }
}

// Global instance
let accountSwitcher = null;

// Auto-initialize on DOM load
document.addEventListener('DOMContentLoaded', async () => {
  accountSwitcher = new AccountSwitcher();
  await accountSwitcher.init();
});
