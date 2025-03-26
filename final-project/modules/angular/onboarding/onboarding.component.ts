import { Component, OnInit } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { OnboardingService } from './onboarding.service';

@Component({
  selector: 'app-onboarding',
  template: `
    <div class="onboarding-container">
      <router-outlet></router-outlet>
    </div>
  `,
  styleUrls: ['./onboarding.component.scss'],
  standalone: true,
  imports: [RouterOutlet]
})
export class OnboardingComponent implements OnInit {
  constructor(
    private router: Router,
    private onboardingService: OnboardingService
  ) { }

  ngOnInit(): void {
    // Check if already initialized and redirect if needed
    this.onboardingService.getStatus().subscribe(status => {
      if (status.is_initialized) {
        this.router.navigate(['/']);
      }
    });
  }
}
