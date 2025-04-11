import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { VocabularyService, Word } from '../../services/vocabulary.service';

@Component({
  selector: 'app-vocabulary',
  standalone: true,
  imports: [CommonModule, RouterLink, ReactiveFormsModule],
  template: `
    <div class="vocabulary-page">
      <header class="page-header">
        <h1>Vocabulary List</h1>
        <div class="search-box">
          <input
            type="text"
            [formControl]="searchControl"
            placeholder="Search by word or meaning..."
            class="search-input"
          />
        </div>
      </header>

      <div class="vocabulary-grid" *ngIf="!loading && !error">
        <div class="vocabulary-card" 
          *ngFor="let word of wordList"
          [routerLink]="['/vocabulary', word.id]">
          <div class="word">{{ word.japanese }}</div>
          <div class="details">
            <div class="meaning">{{ word.english }}</div>
            <div class="reading">{{ word.kana }}</div>
            <div class="romaji">{{ word.romaji }}</div>
          </div>
        </div>
      </div>

      <div class="loading" *ngIf="loading">
        Loading vocabulary...
      </div>

      <div class="error" *ngIf="error">
        {{ error }}
      </div>

      <div class="pagination" *ngIf="!loading && !error && totalItems > 0">
        <button 
          [disabled]="currentPage === 1"
          (click)="changePage(currentPage - 1)">
          Previous
        </button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button 
          [disabled]="currentPage === totalPages"
          (click)="changePage(currentPage + 1)">
          Next
        </button>
      </div>
    </div>
  `,
  styleUrls: ['./vocabulary.component.scss']
})
export class VocabularyComponent implements OnInit {
  wordList: Word[] = [];
  loading = true;
  error: string | null = null;
  currentPage = 1;
  totalItems = 0;
  totalPages = 0;
  searchControl = new FormControl('');

  constructor(private vocabularyService: VocabularyService) {}

  ngOnInit() {
    this.loadWords();
    this.setupSearch();
  }

  private setupSearch() {
    this.searchControl.valueChanges.pipe(
      debounceTime(300),
      distinctUntilChanged()
    ).subscribe(term => {
      this.currentPage = 1; // Reset to first page when searching
      this.loadWords(term || undefined);
    });
  }

  async loadWords(search?: string) {
    try {
      this.loading = true;
      this.error = null;
      const result = await this.vocabularyService.getWordList(this.currentPage, search);
      this.wordList = result.items;
      this.totalItems = result.pagination.total_items;
      this.totalPages = result.pagination.total_pages;
      this.currentPage = result.pagination.current_page;
    } catch (err) {
      this.error = 'Failed to load vocabulary. Please try again later.';
      console.error('Error loading vocabulary:', err);
    } finally {
      this.loading = false;
    }
  }

  changePage(page: number) {
    this.currentPage = page;
    this.loadWords(this.searchControl.value || undefined);
  }
}
