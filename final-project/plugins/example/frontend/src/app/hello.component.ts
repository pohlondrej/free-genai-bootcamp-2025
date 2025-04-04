import { Component, OnDestroy, OnInit } from '@angular/core';

@Component({
  selector: 'plugin-hello',
  standalone: true,
  template: `
    <div class="plugin-hello">
      <h2>Hello from Example Plugin!</h2>
      <p>This component was loaded via Module Federation.</p>
    </div>
  `,
  styles: [`
    .plugin-hello {
      padding: 20px;
      border: 2px solid #4CAF50;
      border-radius: 8px;
      margin: 20px;
    }
  `]
})
export class HelloComponent implements OnInit, OnDestroy {
  constructor() {
    console.log('HelloComponent: Constructor');
  }

  ngOnInit(): void {
    console.log('HelloComponent: OnInit');
  }

  ngOnDestroy(): void {
    console.log('HelloComponent: OnDestroy');
  }
}
