import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormControl } from '@angular/forms';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { GroupsService, Group } from '../../../services/groups.service';

@Component({
  selector: 'app-duoradio',
  standalone: false,
  templateUrl: './duoradio.component.html',
  styleUrls: ['./duoradio.component.scss']
})
export class DuoRadioComponent implements OnInit {
  searchControl = new FormControl('');
  groups: Group[] = [];
  filteredGroups: Group[] = [];
  stats = {
    totalCards: 0,
    cardsStudied: 0,
    successRate: 0
  };

  constructor(
    private groupsService: GroupsService,
    private router: Router,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    this.loadGroups();
    this.setupSearch();
    // TODO: Load actual stats from service
    this.stats = {
      totalCards: 1000,
      cardsStudied: 250,
      successRate: 85
    };
  }

  private async loadGroups() {
    try {
      const response = await this.groupsService.getGroupList(1);
      this.groups = response.items;
      this.filterGroups('');
    } catch (error) {
      console.error('Error loading groups:', error);
      // TODO: Show error message to user
    }
  }

  private setupSearch() {
    this.searchControl.valueChanges.pipe(
      debounceTime(300),
      distinctUntilChanged()
    ).subscribe(term => {
      this.filterGroups(term || '');
    });
  }

  private filterGroups(term: string) {
    const searchTerm = term.toLowerCase();
    this.filteredGroups = this.groups.filter(group =>
      group.name.toLowerCase().includes(searchTerm)
    );
  }

  startSession(group: Group) {
    this.router.navigate(['play', group.id], { relativeTo: this.route });
  }
}
