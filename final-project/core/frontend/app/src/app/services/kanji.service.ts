import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';

export interface KanjiStats {
  total_reviews: number;
  correct_reviews: number;
  wrong_reviews: number;
}

export interface KanjiGroup {
  id: number;
  name: string;
}

export interface Kanji {
  id: number;
  kanji_level: string;
  symbol: string;
  primary_meaning: string;
  primary_reading: string;
  primary_reading_type: 'on' | 'kun';
  stats: KanjiStats;
  groups?: KanjiGroup[];
}

export interface PaginationInfo {
  current_page: number;
  total_pages: number;
  total_items: number;
  items_per_page: number;
}

export interface KanjiListResponse {
  items: Kanji[];
  pagination: PaginationInfo;
}

@Injectable({
  providedIn: 'root'
})
export class KanjiService {
  private apiUrl = '/api';

  constructor(private http: HttpClient) {}

  async getKanjiList(page: number = 1): Promise<KanjiListResponse> {
    const params = new URLSearchParams({
      page: page.toString()
    });
    
    return firstValueFrom(
      this.http.get<KanjiListResponse>(`${this.apiUrl}/kanji?${params}`)
    );
  }

  async getKanjiById(id: number): Promise<Kanji> {
    return firstValueFrom(
      this.http.get<Kanji>(`${this.apiUrl}/kanji/${id}`)
    );
  }
}
