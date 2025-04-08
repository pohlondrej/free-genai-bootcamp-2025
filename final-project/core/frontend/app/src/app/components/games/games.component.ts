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
        <p class="subtitle">Explore interactive ways to learn Japanese</p>
      </header>

      <div class="games-grid" *ngIf="!loading && !error">
        <div class="game-card"
          *ngFor="let game of games"
          [routerLink]="['/games', game.id]">
          <div class="game-image">
            <img 
              [src]="game.backend_endpoint + '/image'"
              (error)="onImageError($event)"
              alt="Preview of {{ game.name }}"
            >
          </div>
          <div class="game-content">
            <h2 class="name">{{ game.name }}</h2>
            <p class="description">{{ game.description }}</p>
          </div>
        </div>
      </div>

      <div class="loading" *ngIf="loading">
        Loading available games...
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

  constructor(private gamesService: GamesService) {}

  ngOnInit() {
    this.gamesService.games$.subscribe(
      games => {
        this.games = games;
        this.loading = false;
      },
      error => {
        this.error = 'Failed to load games. Please try again later.';
        this.loading = false;
        console.error('Error loading games:', error);
      }
    );
  }

  onImageError(event: Event) {
    const img = event.target as HTMLImageElement;
    img.src = '/assets/crabowl_background.svg';
  }
}
