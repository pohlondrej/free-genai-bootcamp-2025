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

export interface GroupDetails {
  id: number;
  name: string;
  stats: {
    total_items: number;
    word_count: number;
    kanji_count: number;
    completed_sessions: number;
    active_sessions: number;
  };
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
}
