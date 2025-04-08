import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

export interface StudySession {
  id: number;
  activity_type: string;
  group_name: string;
  created_at: string;
  completed_at: string | null;
  review_items_count: number;
  group_id: number;
  review_items: any[];
}

@Injectable({
  providedIn: 'root'
})
export class StudySessionsService {
  private apiUrl = `${environment.apiUrl}/study-sessions`;

  constructor(private http: HttpClient) { }

  startSession(groupId: number, activityType: string) {
    return this.http.post<StudySession>(this.apiUrl, {
      group_id: groupId,
      activity_type: activityType
    });
  }

  endSession(sessionId: number) {
    return this.http.post<StudySession>(`${this.apiUrl}/${sessionId}/end`, {});
  }
}
