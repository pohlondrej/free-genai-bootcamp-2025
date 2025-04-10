import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { DuoRadioComponent } from './duoradio.component';
import { DuoRadioGameComponent } from './duoradio-game.component';
import { HttpClientModule } from '@angular/common/http';

const routes: Routes = [
  {
    path: '',
    component: DuoRadioComponent
  },
  {
    path: 'play/:groupId',
    component: DuoRadioGameComponent
  }
];

@NgModule({
  declarations: [
    DuoRadioComponent,
    DuoRadioGameComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    RouterModule.forChild(routes)
  ],
  exports: [RouterModule]
})
export class DuoRadioModule {}
