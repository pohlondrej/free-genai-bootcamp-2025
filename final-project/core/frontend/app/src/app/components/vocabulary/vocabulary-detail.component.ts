import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { VocabularyService, Word } from '../../services/vocabulary.service';

@Component({
  selector: 'app-vocabulary-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="vocabulary-detail-page">
      <header class="page-header">
        <button class="back-button" routerLink="/vocabulary">← Back to List</button>
      </header>

      <div class="vocabulary-detail" *ngIf="!loading && !error && word">
        <div class="word-main">
          <div class="word-info">
            <div class="japanese">{{ word.japanese }}</div>
            <div class="readings">
              <div class="kana">{{ word.kana }}</div>
              <div class="romaji">{{ word.romaji }}</div>
            </div>
            <div class="english">{{ word.english }}</div>
            <div class="level">{{ word.word_level }}</div>
          </div>
        </div>

        <div class="stats">
          <h2>Stats</h2>
          <div class="stats-grid">
            <div class="stat">
              <div class="label">Total Reviews</div>
              <div class="value">{{ word.stats.total_reviews }}</div>
            </div>
            <div class="stat">
              <div class="label">Correct</div>
              <div class="value correct">{{ word.stats.correct_reviews }}</div>
            </div>
            <div class="stat">
              <div class="label">Wrong</div>
              <div class="value wrong">{{ word.stats.wrong_reviews }}</div>
            </div>
          </div>
        </div>

        <div class="groups" *ngIf="word.groups?.length">
          <h2>Groups</h2>
          <div class="group-list">
            <div class="group" *ngFor="let group of word.groups">
              {{ group.name }}
            </div>
          </div>
        </div>
      </div>

      <div class="loading" *ngIf="loading">
        Loading word...
      </div>

      <div class="error" *ngIf="error">
        {{ error }}
      </div>
    </div>
  `,
  styleUrls: ['./vocabulary-detail.component.scss']
})
export class VocabularyDetailComponent implements OnInit {
  word: Word | null = null;
  loading = true;
  error: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private vocabularyService: VocabularyService
  ) {}

  ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (isNaN(id)) {
      this.router.navigate(['/vocabulary']);
      return;
    }
    this.loadWord(id);
  }

  private async loadWord(id: number) {
    try {
      this.loading = true;
      this.error = null;
      this.word = await this.vocabularyService.getWordById(id);
    } catch (err) {
      this.error = 'Failed to load word. Please try again later.';
      console.error('Error loading word:', err);
    } finally {
      this.loading = false;
    }
  }
}
