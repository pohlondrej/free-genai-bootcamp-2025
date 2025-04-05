import { NgModule, OnDestroy, OnInit } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { HelloComponent } from './hello.component';


const routes: Routes = [
  {
    path: '',
    component: HelloComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HelloRoutingModule implements OnInit, OnDestroy {
    constructor() {
      console.log('HelloRoutingModule: Constructor');
    }
  
    ngOnInit(): void {
      console.log('HelloRoutingModule: OnInit');
    }
  
    ngOnDestroy(): void {
      console.log('HelloRoutingModule: OnDestroy');
    }
  }
  