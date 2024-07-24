import { Component } from '@angular/core';

interface App {
  name: string;
  link: string;
  image: string;
}

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  searchText = '';
  apps: App[] = [
      { name: 'CAPITAL-BANKER', link: 'https://django-jenkins.readthedocs.io/en/latest/#getting-started', image: 'assets/icons/cbs.jpeg' },
      { name: 'AUB-DOC', link: '/appliaub:8082/login', image: 'assets/icons/computer-network.png' },
      { name: 'GEC/GED', link: '/appli/bac-cheque', image: 'assets/icons/folders.png' },
      { name: 'ASANA', link: 'https://app.asana.com/-/login?_gl=1*j90sd6*_gcl_au*MTQ4NzkyNDgzNy4xNzIxNzUyMzcy*FPAU*MTQ4NzkyNDgzNy4xNzIxNzUyMzcy*_ga*ODQyNDk2ODIyLjE3MjE3NTIzNzI.*_ga_J1KDXMCQTH*MTcyMTc1MjM3MS4xLjEuMTcyMTc1MjM3NC41Ny4wLjYxMTU4MzE3Mw..*_fplc*U0F0VFVjaW5YdnpFT05sa0pzYlI1UzdXeHBxSVc3YXFJaTQ4S1QxWGElMkJwa3I0dkVocFJYT2dJdlFNb2tydG5PdnV0S1lmZVR3NUM2dVNlNWRvSmowNTMlMkZIMDNFaFJETVNvRFNwbW1UVWlPb1BIN3VEV0NWenN2Rkg4OGRGUSUzRCUzRA..', image: 'assets/icons/asana.png' }
  ];
  filteredApps: App[] = [];

  constructor() {
      this.filteredApps = this.apps;
  }

  search() {
      if (this.searchText.trim() === '') {
          this.filteredApps = this.apps;
      } else {
          this.filteredApps = this.apps.filter(app =>
              app.name.toLowerCase().includes(this.searchText.trim().toLowerCase())
          );
      }
  }
}
