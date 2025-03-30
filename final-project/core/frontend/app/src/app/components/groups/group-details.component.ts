import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { GroupsService, GroupDetails } from '../../services/groups.service';

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

        <!-- TODO: Add list of items in the group -->
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
  loading = true;
  error: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private groupsService: GroupsService
  ) {}

  ngOnInit() {
    const groupId = this.route.snapshot.paramMap.get('id');
    if (groupId) {
      this.loadGroupDetails(parseInt(groupId, 10));
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
}
