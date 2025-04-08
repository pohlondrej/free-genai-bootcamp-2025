import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

interface ReviewItem {
  item_type: string;
  item_id: number;
  study_session_id: number;
  correct: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class ReviewService {
  private apiUrl = `${environment.apiUrl}/review`;

  constructor(private http: HttpClient) { }

  createReview(review: ReviewItem) {
    return this.http.post(`${this.apiUrl}/create`, review);
  }
}
