import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-welcome',
  templateUrl: './welcome.component.html',
  styleUrls: ['./welcome.component.scss'],
  standalone: true,
  imports: [RouterModule]
})
export class WelcomeComponent {
  constructor(private router: Router) { }

  startOnboarding(): void {
    this.router.navigate(['onboarding/wizard']);
  }
}
