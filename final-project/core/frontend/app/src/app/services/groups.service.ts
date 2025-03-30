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
}
