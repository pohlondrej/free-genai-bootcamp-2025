import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { firstValueFrom } from 'rxjs';

export interface StudyProgress {
  total_words: number;
  studied_words: number;
  total_kanji: number;
  studied_kanji: number;
}

export interface WanikaniLevel {
  level: number;
}

export interface StudyItem {
  id: number;
  type: string;
  count?: number;
  success_rate?: number;
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
}

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  private apiUrl = `${environment.apiUrl}/dashboard`;

  constructor(private http: HttpClient) {}

  async getStudyProgress(): Promise<StudyProgress> {
    return firstValueFrom(this.http.get<StudyProgress>(`${this.apiUrl}/study-progress`));
  }

  async getWanikaniLevel(): Promise<WanikaniLevel | null> {
    try {
      return await firstValueFrom(this.http.get<WanikaniLevel>(`${this.apiUrl}/wanikani-level`));
    } catch {
      return null;
    }
  }

  async getMostStudied(limit: number = 5): Promise<StudyItem[]> {
    const result = await firstValueFrom(
      this.http.get<StudyItem[]>(`${this.apiUrl}/most-studied?limit=${limit}`)
    );
    return result || [];
  }

  async getProblematicItems(limit: number = 5): Promise<StudyItem[]> {
    const result = await firstValueFrom(
      this.http.get<StudyItem[]>(`${this.apiUrl}/problematic-items?limit=${limit}`)
    );
    return result || [];
  }

  async getMostStudiedGroup(): Promise<GroupStats | null> {
    try {
      return await firstValueFrom(this.http.get<GroupStats>(`${this.apiUrl}/most-studied-group`));
    } catch {
      return null;
    }
  }

  async getLastStudied(): Promise<LastStudied | null> {
    try {
      return await firstValueFrom(this.http.get<LastStudied>(`${this.apiUrl}/last-studied`));
    } catch {
      return null;
    }
  }
}
