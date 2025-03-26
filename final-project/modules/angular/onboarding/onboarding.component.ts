import { Component, OnInit } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { OnboardingService } from './onboarding.service';

@Component({
  selector: 'app-onboarding',
  template: '<router-outlet></router-outlet>',
  standalone: true,
  imports: [RouterOutlet]
})
export class OnboardingComponent implements OnInit {
  constructor(
    private onboardingService: OnboardingService,
    private router: Router
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
