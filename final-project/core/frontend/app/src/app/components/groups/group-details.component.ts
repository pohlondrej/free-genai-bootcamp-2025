import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { GroupsService, GroupDetails, GroupItem, PaginatedResponse } from '../../services/groups.service';

@Component({
  selector: 'app-group-details',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="group-details-page">
      <header class="page-header">
        <a routerLink="/groups" class="back-link">← Back to Groups</a>
        <h1>{{ group?.name }}</h1>
      </header>

      <div class="group-content" *ngIf="!loading && !error && group">
        <div class="stats-grid">
          <div class="stat-card total">
            <div class="value">{{ group.stats.total_items }}</div>
            <div class="label">Total Items</div>
          </div>
          <div class="stat-card" *ngIf="group.stats.kanji_count">
            <div class="value">{{ group.stats.kanji_count }}</div>
            <div class="label">Kanji</div>
          </div>
          <div class="stat-card" *ngIf="group.stats.word_count">
            <div class="value">{{ group.stats.word_count }}</div>
            <div class="label">Words</div>
          </div>
          <div class="stat-card">
            <div class="value">{{ group.stats.completed_sessions }}</div>
            <div class="label">Completed Sessions</div>
          </div>
          <div class="stat-card">
            <div class="value">{{ group.stats.active_sessions }}</div>
            <div class="label">Active Sessions</div>
          </div>
        </div>

        <div class="items-section">
          <h2>Items</h2>
          <div class="items-grid" *ngIf="items?.length">
            <div class="item-card" *ngFor="let item of items" [routerLink]="['/', item.item_type, item.id]">
              <div class="item-name">{{ item.name }}</div>
              <div class="item-info">
                <span class="item-type">{{ item.item_type }}</span>
                <span class="item-level">{{ item.level }}</span>
              </div>
              <div class="item-stats">
                <div class="stat">
                  <span class="label">Total:</span>
                  <span class="value">{{ item.total_reviews }}</span>
                </div>
                <div class="stat correct">
                  <span class="label">Correct:</span>
                  <span class="value">{{ item.correct_reviews }}</span>
                </div>
                <div class="stat wrong">
                  <span class="label">Wrong:</span>
                  <span class="value">{{ item.wrong_reviews }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="pagination" *ngIf="pagination">
            <button 
              class="prev" 
              [disabled]="pagination.current_page === 1"
              (click)="loadPage(pagination.current_page - 1)"
            >
              Previous
            </button>
            <span class="page-info">
              Page {{ pagination.current_page }} of {{ pagination.total_pages }}
            </span>
            <button 
              class="next"
              [disabled]="pagination.current_page === pagination.total_pages"
              (click)="loadPage(pagination.current_page + 1)"
            >
              Next
            </button>
          </div>
        </div>
      </div>

      <div class="loading" *ngIf="loading">
        Loading group details...
      </div>

      <div class="error" *ngIf="error">
        {{ error }}
      </div>
    </div>
  `,
  styleUrls: ['./group-details.component.scss']
})
export class GroupDetailsComponent implements OnInit {
  group: GroupDetails | null = null;
  items: GroupItem[] = [];
  pagination: PaginatedResponse<GroupItem>['pagination'] | null = null;
  loading = true;
  error: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private groupsService: GroupsService
  ) {}

  ngOnInit() {
    const groupId = this.route.snapshot.paramMap.get('id');
    if (groupId) {
      const id = parseInt(groupId, 10);
      this.loadGroupDetails(id);
      this.loadItems(id);
    } else {
      this.error = 'Group ID not found';
      this.loading = false;
    }
  }

  async loadGroupDetails(id: number) {
    try {
      this.loading = true;
      this.error = null;
      this.group = await this.groupsService.getGroup(id);
    } catch (err) {
      this.error = 'Failed to load group details. Please try again later.';
      console.error('Error loading group details:', err);
    } finally {
      this.loading = false;
    }
  }

  async loadItems(groupId: number, page: number = 1) {
    try {
      const response = await this.groupsService.getGroupItems(groupId, page);
      this.items = response.items;
      this.pagination = response.pagination;
    } catch (err) {
      console.error('Error loading group items:', err);
      // Don't show error to user since this is not critical
    }
  }

  async loadPage(page: number) {
    const groupId = this.route.snapshot.paramMap.get('id');
    if (groupId) {
      await this.loadItems(parseInt(groupId, 10), page);
    }
  }
}
