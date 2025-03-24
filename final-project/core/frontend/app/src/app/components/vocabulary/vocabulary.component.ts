import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-vocabulary',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="vocabulary">
      <h1>Vocabulary</h1>
      <p>Your vocabulary list will appear here.</p>
    </div>
  `,
  styleUrls: ['./vocabulary.component.scss']
})
export class VocabularyComponent {}
