import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-kanji',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="kanji">
      <h1>Kanji</h1>
      <p>Your kanji list will appear here.</p>
    </div>
  `,
  styleUrls: ['./kanji.component.scss']
})
export class KanjiComponent {}
