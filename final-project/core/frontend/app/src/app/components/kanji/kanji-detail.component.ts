import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { KanjiService, Kanji } from '../../services/kanji.service';

@Component({
  selector: 'app-kanji-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="kanji-detail-page">
      <header class="page-header">
        <button class="back-button" routerLink="/kanji">← Back to List</button>
      </header>

      <div class="kanji-detail" *ngIf="!loading && !error && kanji">
        <div class="kanji-main">
          <div class="character">{{ kanji.symbol }}</div>
          <div class="info">
            <h1 class="meaning">{{ kanji.primary_meaning }}</h1>
            <div class="reading">
              {{ getReadingType(kanji.primary_reading_type) }}: {{ kanji.primary_reading }}
            </div>
            <div class="level">{{ kanji.kanji_level }}</div>
          </div>
        </div>

        <div class="stats">
          <h2>Stats</h2>
          <div class="stats-grid">
            <div class="stat">
              <div class="label">Total Reviews</div>
              <div class="value">{{ kanji.stats.total_reviews }}</div>
            </div>
            <div class="stat">
              <div class="label">Correct</div>
              <div class="value correct">{{ kanji.stats.correct_reviews }}</div>
            </div>
            <div class="stat">
              <div class="label">Wrong</div>
              <div class="value wrong">{{ kanji.stats.wrong_reviews }}</div>
            </div>
          </div>
        </div>

        <div class="groups" *ngIf="kanji.groups?.length">
          <h2>Groups</h2>
          <div class="group-list">
            <div class="group" *ngFor="let group of kanji.groups" [routerLink]="['/groups', group.id]">
              {{ group.name }}
            </div>
          </div>
        </div>
      </div>

      <div class="loading" *ngIf="loading">
        Loading kanji...
      </div>

      <div class="error" *ngIf="error">
        {{ error }}
      </div>
    </div>
  `,
  styleUrls: ['./kanji-detail.component.scss']
})
export class KanjiDetailComponent implements OnInit {
  kanji: Kanji | null = null;
  loading = true;
  error: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private kanjiService: KanjiService
  ) {}

  ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (isNaN(id)) {
      this.router.navigate(['/kanji']);
      return;
    }
    this.loadKanji(id);
  }

  private async loadKanji(id: number) {
    try {
      this.loading = true;
      this.error = null;
      this.kanji = await this.kanjiService.getKanjiById(id);
    } catch (err) {
      this.error = 'Failed to load kanji. Please try again later.';
      console.error('Error loading kanji:', err);
    } finally {
      this.loading = false;
    }
  }

  getReadingType(type: 'on' | 'kun'): string {
    return type === 'on' ? "On'yomi" : "Kun'yomi";
  }
}
