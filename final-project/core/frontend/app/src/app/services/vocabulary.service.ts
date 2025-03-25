import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';

export interface WordStats {
  total_reviews: number;
  correct_reviews: number;
  wrong_reviews: number;
}

export interface WordGroup {
  id: number;
  name: string;
}

export interface Word {
  id: number;
  word_level: string;
  japanese: string;
  kana: string;
  romaji: string;
  english: string;
  stats: WordStats;
  groups?: WordGroup[];
}

export interface PaginationInfo {
  current_page: number;
  total_pages: number;
  total_items: number;
  items_per_page: number;
}

export interface WordListResponse {
  items: Word[];
  pagination: PaginationInfo;
}

@Injectable({
  providedIn: 'root'
})
export class VocabularyService {
  private apiUrl = '/api';

  constructor(private http: HttpClient) {}

  async getWordList(page: number = 1): Promise<WordListResponse> {
    const params = new URLSearchParams({
      page: page.toString()
    });
    
    return firstValueFrom(
      this.http.get<WordListResponse>(`${this.apiUrl}/words?${params}`)
    );
  }

  async getWordById(id: number): Promise<Word> {
    return firstValueFrom(
      this.http.get<Word>(`${this.apiUrl}/words/${id}`)
    );
  }
}
