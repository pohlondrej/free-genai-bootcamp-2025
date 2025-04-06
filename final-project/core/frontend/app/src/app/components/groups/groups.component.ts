import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { GroupsService, Group } from '../../services/groups.service';

@Component({
  selector: 'app-groups',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="groups-page">
      <header class="page-header">
        <h1>Study Groups</h1>
      </header>

      <div class="groups-grid" *ngIf="!loading && !error">
        <div class="group-card" 
          *ngFor="let group of groupList"
          [routerLink]="['/groups', group.id]">
          <div class="name">{{ group.name }}</div>
          <div class="stats">
            <div class="stat" *ngIf="group.kanji_count > 0">
              <span class="label">Kanji:</span>
              <span class="value">{{ group.kanji_count }}</span>
            </div>
            <div class="stat" *ngIf="group.word_count > 0">
              <span class="label">Words:</span>
              <span class="value">{{ group.word_count }}</span>
            </div>
            <div class="stat total">
              <span class="label">Total:</span>
              <span class="value">{{ group.total_items }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="loading" *ngIf="loading">
        Loading groups...
      </div>

      <div class="error" *ngIf="error">
        {{ error }}
      </div>

      <div class="pagination" *ngIf="!loading && !error && totalItems > 0">
        <button 
          [disabled]="currentPage === 1"
          (click)="changePage(currentPage - 1)">
          Previous
        </button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button 
          [disabled]="currentPage === totalPages"
          (click)="changePage(currentPage + 1)">
          Next
        </button>
      </div>
    </div>
  `,
  styleUrls: ['./groups.component.scss']
})
export class GroupsComponent implements OnInit {
  groupList: Group[] = [];
  loading = true;
  error: string | null = null;
  currentPage = 1;
  totalItems = 0;
  totalPages = 0;

  constructor(private groupsService: GroupsService) {}

  ngOnInit() {
    this.loadGroups();
  }

  async loadGroups() {
    try {
      this.loading = true;
      this.error = null;
      const result = await this.groupsService.getGroupList(this.currentPage);
      this.groupList = result.items;
      this.totalItems = result.pagination.total_items;
      this.totalPages = result.pagination.total_pages;
      this.currentPage = result.pagination.current_page;
    } catch (err) {
      this.error = 'Failed to load groups. Please try again later.';
      console.error('Error loading groups:', err);
    } finally {
      this.loading = false;
    }
  }

  changePage(page: number) {
    this.currentPage = page;
    this.loadGroups();
  }
}
