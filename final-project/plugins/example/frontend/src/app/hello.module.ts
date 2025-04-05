import { NgModule, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HelloComponent } from './hello.component';
import { HelloRoutingModule } from './hello-routing.module';

@NgModule({
  imports: [CommonModule, HelloRoutingModule], 
  declarations: [HelloComponent]
})
export class HelloModule implements OnInit, OnDestroy {
  constructor() {
    console.log('HelloModule: Constructor');
  }

  ngOnInit(): void {
    console.log('HelloModule: OnInit');
  }

  ngOnDestroy(): void {
    console.log('HelloModule: OnDestroy');
  }
}