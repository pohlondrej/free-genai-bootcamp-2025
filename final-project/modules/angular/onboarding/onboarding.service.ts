import { Injectable } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@env/environment';

export interface OnboardingStatus {
  is_initialized: boolean;
  message?: string;
}

export interface OnboardingConfig {
  api_key: string;
  gemini_api_key?: string;
  use_wanikani: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class OnboardingService {
  private apiUrl = `${environment.apiUrl}/onboarding`;

  constructor(private http: HttpClient) { }

  getStatus(): Observable<OnboardingStatus> {
    return this.http.get<OnboardingStatus>(`${this.apiUrl}/status`);
  }

  initialize(config: OnboardingConfig): Observable<OnboardingStatus> {
    return this.http.post<OnboardingStatus>(`${this.apiUrl}/initialize`, config);
  }
}
