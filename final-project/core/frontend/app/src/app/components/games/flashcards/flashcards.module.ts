import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FlashcardsComponent } from './flashcards.component';
import { FlashcardGameComponent } from './flashcard-game.component';

const routes: Routes = [
  {
    path: '',
    component: FlashcardsComponent,
    children: [
      {
        path: 'play/:groupId',
        component: FlashcardGameComponent
      }
    ]
  }
];

@NgModule({
  declarations: [
    FlashcardsComponent,
    FlashcardGameComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule.forChild(routes)
  ],
  exports: [RouterModule]
})
export class FlashcardsModule {}
