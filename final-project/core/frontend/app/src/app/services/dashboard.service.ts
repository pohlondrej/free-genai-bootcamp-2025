import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { Word, VocabularyService } from './vocabulary.service';
import { Kanji, KanjiService } from './kanji.service';

export interface WanikaniLevel {
  level: number;
}

export interface StudyProgress {
  total_words: number;
  total_kanji: number;
  studied_words: number;
  studied_kanji: number;
}

export interface StudyItem {
  id: number;
  type: string;
  count?: number;
  success_rate?: number;
  details?: Word | Kanji;  
}

export interface GroupStats {
  id: number;
  name: string;
  activity_count: number;
}

export interface LastStudied {
  item_id: number;
  item_type: string;
  studied_at: string;
  details?: Word | Kanji;  
}

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  private apiUrl = '/api';

  constructor(
    private http: HttpClient,
    private vocabularyService: VocabularyService,
    private kanjiService: KanjiService
  ) {}

  async getStudyProgress(): Promise<StudyProgress> {
    return firstValueFrom(
      this.http.get<StudyProgress>(`${this.apiUrl}/dashboard/study-progress`)
    );
  }

  async getWanikaniLevel(): Promise<WanikaniLevel | null> {
    try {
      return await firstValueFrom(
        this.http.get<WanikaniLevel>(`${this.apiUrl}/dashboard/wanikani-level`)
      );
    } catch {
      return null;
    }
  }

  async getMostStudied(): Promise<StudyItem[]> {
    const items = await firstValueFrom(
      this.http.get<StudyItem[]>(`${this.apiUrl}/dashboard/most-studied?limit=5`)
    );
    return await this.loadItemDetails(items);
  }

  async getProblematicItems(): Promise<StudyItem[]> {
    const items = await firstValueFrom(
      this.http.get<StudyItem[]>(`${this.apiUrl}/dashboard/problematic-items?limit=5`)
    );
    return await this.loadItemDetails(items);
  }

  async getMostStudiedGroup(): Promise<GroupStats | null> {
    try {
      return await firstValueFrom(
        this.http.get<GroupStats>(`${this.apiUrl}/dashboard/most-studied-group`)
      );
    } catch {
      return null;
    }
  }

  async getLastStudied(): Promise<LastStudied | null> {
    try {
      const lastStudied = await firstValueFrom(
        this.http.get<LastStudied>(`${this.apiUrl}/dashboard/last-studied`)
      );
      
      // Load item details
      if (lastStudied.item_type === 'word') {
        lastStudied.details = await this.vocabularyService.getWordById(lastStudied.item_id);
      } else if (lastStudied.item_type === 'kanji') {
        lastStudied.details = await this.kanjiService.getKanjiById(lastStudied.item_id);
      }
      
      return lastStudied;
    } catch {
      return null;
    }
  }

  private async loadItemDetails(items: StudyItem[]): Promise<StudyItem[]> {
    // Load details for each item in parallel
    const itemsWithDetails = await Promise.all(
      items.map(async (item) => {
        try {
          if (item.type === 'word') {
            item.details = await this.vocabularyService.getWordById(item.id);
          } else if (item.type === 'kanji') {
            item.details = await this.kanjiService.getKanjiById(item.id);
          }
        } catch (error) {
          console.error(`Error loading details for ${item.type} ${item.id}:`, error);
        }
        return item;
      })
    );
    
    return itemsWithDetails;
  }
}
