import { NgModule, OnDestroy, OnInit } from '@angular/core';
import { HelloComponent } from './hello.component';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: '',
    component: HelloComponent
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)], 
  exports: [RouterModule]
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