import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { GamesService, GameInfo } from '../../services/games.service';

@Component({
  selector: 'app-games',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="games-page">
      <header class="page-header">
        <h1>Games</h1>
      </header>

      <div class="games-grid" *ngIf="!loading && !error">
        <div class="game-card"
          *ngFor="let game of games"
          [routerLink]="['/games', game.name]">
          <div class="name">{{ game.name }}</div>
        </div>
      </div>

      <div class="loading" *ngIf="loading">
        Loading games...
      </div>

      <div class="error" *ngIf="error">
        {{ error }}
      </div>
    </div>
  `,
  styleUrls: ['./games.component.scss']
})
export class GamesComponent implements OnInit {
  games: GameInfo[] = [];
  loading = true;
  error: string | null = null;

  constructor(private gamesService: GamesService, private router: Router) {}

  ngOnInit() {
    this.loadGames();
  }

  private loadGames() {
    this.gamesService.getGames().subscribe({
      next: (games) => {
        this.games = games;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load games. Please try again later.';
        this.loading = false;
        console.error('Error loading games:', err);
      }
    });
  }
}
