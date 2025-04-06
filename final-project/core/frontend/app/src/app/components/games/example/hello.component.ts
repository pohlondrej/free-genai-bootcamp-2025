import { Component, OnDestroy, OnInit, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'plugin-hello',
  standalone: false,
  encapsulation: ViewEncapsulation.None,
  template: `
    <div class="plugin-hello">
      <h2>Hello from Example Plugin!</h2>
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

  ngDoCheck(): void {
    console.log('HelloComponent: Change detection triggered');
  }
}
