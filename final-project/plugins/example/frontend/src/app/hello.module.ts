import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HelloComponent } from './hello.component';

@NgModule({
  imports: [
    CommonModule,
    HelloComponent // Import the standalone component
  ],
  exports: [
    HelloComponent // Export the standalone component
  ]
})
export class HelloModule { }