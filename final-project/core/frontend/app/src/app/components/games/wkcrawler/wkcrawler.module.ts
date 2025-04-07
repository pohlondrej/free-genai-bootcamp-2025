import { NgModule, OnDestroy, OnInit } from '@angular/core';
import { WkCrawlerComponent } from './wkcrawler.component';
import { RouterModule, Routes } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

const routes: Routes = [
  {
    path: '',
    component: WkCrawlerComponent
  }
];

@NgModule({
  declarations: [WkCrawlerComponent],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule.forChild(routes)
  ],
  exports: [RouterModule]
})
export class WkCrawlerModule implements OnInit, OnDestroy {
  constructor() {
    console.log('WkCrawlerModule: Constructor');
  }

  ngOnInit(): void {
    console.log('WkCrawlerModule: OnInit');
  }

  ngOnDestroy(): void {
    console.log('WkCrawlerModule: OnDestroy');
  }
}
