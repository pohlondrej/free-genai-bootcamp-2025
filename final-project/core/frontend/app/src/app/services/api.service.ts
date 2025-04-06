import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  async get<T>(path: string): Promise<T> {
    return firstValueFrom(this.http.get<T>(`${this.apiUrl}${path}`));
  }

  async post<T>(path: string, body: any): Promise<T> {
    return firstValueFrom(this.http.post<T>(`${this.apiUrl}${path}`, body));
  }

  async put<T>(path: string, body: any): Promise<T> {
    return firstValueFrom(this.http.put<T>(`${this.apiUrl}${path}`, body));
  }

  async delete<T>(path: string): Promise<T> {
    return firstValueFrom(this.http.delete<T>(`${this.apiUrl}${path}`));
  }
}
