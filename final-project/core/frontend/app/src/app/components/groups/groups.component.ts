import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-groups',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="groups">
      <h1>Study Groups</h1>
      <p>Your study groups will appear here.</p>
    </div>
  `,
  styleUrls: ['./groups.component.scss']
})
export class GroupsComponent {}
