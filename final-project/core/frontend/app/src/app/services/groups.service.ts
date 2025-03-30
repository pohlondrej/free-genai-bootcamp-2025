import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

export interface Group {
  id: number;
  name: string;
  word_count: number;
  kanji_count: number;
  total_items: number;
}

export interface GroupStats {
  total_items: number;
  kanji_count: number;
  word_count: number;
  completed_sessions: number;
  active_sessions: number;
}

export interface GroupDetails {
  id: number;
  name: string;
  stats: GroupStats;
}

export interface GroupItem {
  id: number;
  item_type: 'kanji' | 'word';
  name: string;
  level: string;
  total_reviews: number;
  correct_reviews: number;
  wrong_reviews: number;
}

export interface GroupsResponse {
  items: Group[];
  pagination: {
    current_page: number;
    total_pages: number;
    total_items: number;
    items_per_page: number;
  };
}

export interface PaginatedResponse<T> {
  items: T[];
  pagination: {
    current_page: number;
    total_pages: number;
    total_items: number;
    items_per_page: number;
  };
}

@Injectable({
  providedIn: 'root'
})
export class GroupsService {
  private apiUrl = `${environment.apiUrl}/groups`;

  constructor(private http: HttpClient) {}

  async getGroupList(page: number): Promise<GroupsResponse> {
    const response = await this.http
      .get<GroupsResponse>(`${this.apiUrl}?page=${page}`)
      .toPromise();
    if (!response) {
      throw new Error('Failed to fetch groups');
    }
    return response;
  }

  async getGroup(id: number): Promise<GroupDetails> {
    const response = await this.http
      .get<GroupDetails>(`${this.apiUrl}/${id}`)
      .toPromise();
    if (!response) {
      throw new Error('Failed to fetch group details');
    }
    return response;
  }

  async getGroupItems(groupId: number, page: number = 1): Promise<PaginatedResponse<GroupItem>> {
    const response = await this.http
      .get<PaginatedResponse<GroupItem>>(`${this.apiUrl}/${groupId}/items?page=${page}`)
      .toPromise();
    if (!response) {
      throw new Error('Failed to fetch group items');
    }
    return response;
  }
}
