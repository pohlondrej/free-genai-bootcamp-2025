import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { environment } from '@env/environment';

export interface ImportProgress {
  type: 'import_progress';
  message: string;
  percentage: number;
}

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  private socket: WebSocket | null = null;
  private progressSubject = new Subject<ImportProgress>();

  constructor() {}

  connect(): Observable<ImportProgress> {
    if (!this.socket || this.socket.readyState === WebSocket.CLOSED) {
      // Convert http(s):// to ws(s)://
      const wsUrl = environment.apiUrl.replace(/^http/, 'ws');
      this.socket = new WebSocket(`${wsUrl}/onboarding/progress`);

      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'import_progress') {
          this.progressSubject.next(data as ImportProgress);
        }
      };

      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.progressSubject.error(error);
      };

      this.socket.onclose = () => {
        console.log('WebSocket connection closed');
      };
    }

    return this.progressSubject.asObservable();
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}
