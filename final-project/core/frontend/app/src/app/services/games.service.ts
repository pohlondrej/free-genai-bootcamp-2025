import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';

export interface GameInfo {
  name: string;
  backend_endpoint: string;
  frontend_endpoint: string;
  module_name: string;
  image: string;
}

@Injectable({
  providedIn: 'root'
})
export class GamesService {
  private gamesSubject = new BehaviorSubject<GameInfo[]>([]);
  games$ = this.gamesSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadGames();
  }

  private loadGames() {
    // Games are plugins, at least their backends are
    this.http.get<GameInfo[]>('/api/plugins').subscribe(
      games => this.gamesSubject.next(games)
    );
  }

  getGames(): Observable<GameInfo[]> {
    return this.games$;
  }
}
