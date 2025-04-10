import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { DashboardService, StudyProgress, LastStudied, StudyItem, GroupStats } from '../../services/dashboard.service';
import { Word } from '../../services/vocabulary.service';
import { Kanji } from '../../services/kanji.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="dashboard-page">
      <div class="dashboard-content" *ngIf="!loading">
        <div class="dashboard-grid">
          <!-- Left Column -->
          <div class="main-column">
            <!-- Study Progress -->
            <div class="stats-grid" *ngIf="progress">
              <div class="stat-card total">
                <div class="value">{{ progress.studied_words + progress.studied_kanji }}</div>
                <div class="label">Items Studied</div>
                <div class="sub-label">out of {{ progress.total_words + progress.total_kanji }}</div>
              </div>
              <div class="stat-card words">
                <div class="value">{{ progress.studied_words }}</div>
                <div class="label">Words</div>
                <div class="sub-label">out of {{ progress.total_words }}</div>
              </div>
              <div class="stat-card kanji">
                <div class="value">{{ progress.studied_kanji }}</div>
                <div class="label">Kanji</div>
                <div class="sub-label">out of {{ progress.total_kanji }}</div>
              </div>
              <div class="stat-card wanikani" *ngIf="wanikaniLevel !== null">
                <div class="value">{{ wanikaniLevel }}</div>
                <div class="label">WaniKani Level</div>
              </div>
            </div>

            <!-- Most Studied Items -->
            <div class="items-section" *ngIf="mostStudied?.length">
              <h2>Most Studied Items</h2>
              <div class="items-grid">
                <div class="item-card" *ngFor="let item of mostStudied" [routerLink]="['/', getItemRoute(item.type), item.id]">
                  <div class="item-info">
                    <span class="item-type">{{ getItemDisplayText(item.details, item.type) }}</span>
                    <span class="item-count">{{ item.count }} studies</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column -->
          <div class="side-column">
            <!-- Study Activities -->
            <a routerLink="/games" class="games-button">
              <span class="icon">🎮</span>
              <span class="text">Study Activities</span>
            </a>

            <!-- Most Active Group -->
            <div class="group-section" *ngIf="mostStudiedGroup">
              <h2>Most Active Group</h2>
              <div class="group-card" [routerLink]="['/groups', mostStudiedGroup.id]">
                <div class="group-name">{{ mostStudiedGroup.name }}</div>
                <div class="group-stats">{{ mostStudiedGroup.activity_count }} activities</div>
              </div>
            </div>

            <!-- Last Studied -->
            <div class="items-section" *ngIf="lastStudied">
              <h2>Last Studied</h2>
              <div class="item-card" [routerLink]="['/', getItemRoute(lastStudied.item_type), lastStudied.item_id]">
                <div class="item-info">
                  <span class="item-type">{{ getItemDisplayText(lastStudied.details, lastStudied.item_type) }}</span>
                  <span class="studied-at">{{ lastStudied.studied_at | date:'short' }}</span>
                </div>
              </div>
            </div>

            <!-- Items to Review -->
            <div class="items-section" *ngIf="problematicItems?.length">
              <h2>Items to Review</h2>
              <div class="items-grid">
                <div class="item-card warning" *ngFor="let item of problematicItems" [routerLink]="['/', getItemRoute(item.type), item.id]">
                  <div class="item-info">
                    <span class="item-type">{{ getItemDisplayText(item.details, item.type) }}</span>
                    <span class="item-success">{{ item.success_rate?.toFixed(1) }}% success</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="loading" *ngIf="loading">
        Loading your dashboard...
      </div>
    </div>
  `,
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  loading = true;
  progress: StudyProgress | null = null;
  wanikaniLevel: number | null = null;
  mostStudied: StudyItem[] | null = null;
  problematicItems: StudyItem[] | null = null;
  mostStudiedGroup: GroupStats | null = null;
  lastStudied: LastStudied | null = null;

  constructor(private dashboardService: DashboardService) {}

  async ngOnInit() {
    try {
      const [
        progress,
        wanikani,
        mostStudied,
        problematic,
        group,
        lastStudied
      ] = await Promise.all([
        this.dashboardService.getStudyProgress(),
        this.dashboardService.getWanikaniLevel(),
        this.dashboardService.getMostStudied(),
        this.dashboardService.getProblematicItems(),
        this.dashboardService.getMostStudiedGroup(),
        this.dashboardService.getLastStudied()
      ]);

      this.progress = progress;
      this.wanikaniLevel = wanikani?.level ?? null;
      this.mostStudied = mostStudied;
      this.problematicItems = problematic;
      this.mostStudiedGroup = group;
      this.lastStudied = lastStudied;
    } catch (err) {
      console.error('Error loading dashboard data:', err);
    } finally {
      this.loading = false;
    }
  }

  getItemRoute(itemType: string): string {
    return itemType === 'word' ? 'vocabulary' : itemType;
  }

  getItemType(itemType: string): string {
    return itemType === 'word' ? 'vocabulary' : itemType;
  }

  getItemDisplayText(details: Word | Kanji | undefined, type: string): string {
    if (!details) return this.getItemType(type);
    
    if (type === 'word') {
      return (details as Word).japanese;
    } else if (type === 'kanji') {
      return (details as Kanji).symbol;
    }
    
    return this.getItemType(type);
  }
}
