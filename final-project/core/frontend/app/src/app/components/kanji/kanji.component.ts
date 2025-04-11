import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { KanjiService, Kanji } from '../../services/kanji.service';

@Component({
  selector: 'app-kanji',
  standalone: true,
  imports: [CommonModule, RouterLink, ReactiveFormsModule],
  template: `
    <div class="kanji-page">
      <header class="page-header">
        <h1>Kanji List</h1>
        <div class="search-box">
          <input
            type="text"
            [formControl]="searchControl"
            placeholder="Search by meaning..."
            class="search-input"
          />
        </div>
      </header>

      <div class="kanji-grid" *ngIf="!loading && !error">
        <div class="kanji-card" 
          *ngFor="let kanji of kanjiList"
          [routerLink]="['/kanji', kanji.id]">
          <div class="character">{{ kanji.symbol }}</div>
          <div class="details">
            <div class="meaning">{{ kanji.primary_meaning }}</div>
            <div class="reading">
              {{ kanji.primary_reading }}
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
  styleUrls: ['./kanji.component.scss']
})
export class KanjiComponent implements OnInit {
  kanjiList: Kanji[] = [];
  loading = true;
  error: string | null = null;
  currentPage = 1;
  totalItems = 0;
  totalPages = 0;
  searchControl = new FormControl('');

  constructor(private kanjiService: KanjiService) {}

  ngOnInit() {
    this.loadKanji();
    this.setupSearch();
  }

  private setupSearch() {
    this.searchControl.valueChanges.pipe(
      debounceTime(300),
      distinctUntilChanged()
    ).subscribe(term => {
      this.currentPage = 1; // Reset to first page when searching
      this.loadKanji(term || undefined);
    });
  }

  async loadKanji(search?: string) {
    this.loading = true;
    this.error = null;
    
    try {
      const result = await this.kanjiService.getKanjiList(this.currentPage, search);
      this.kanjiList = result.items;
      this.totalItems = result.pagination.total_items;
      this.totalPages = result.pagination.total_pages;
      this.currentPage = result.pagination.current_page;
    } catch (err) {
      this.error = 'Failed to load kanji. Please try again later.';
      console.error('Error loading kanji:', err);
    } finally {
      this.loading = false;
    }
  }

  changePage(page: number) {
    this.currentPage = page;
    this.loadKanji(this.searchControl.value || undefined);
  }
}
