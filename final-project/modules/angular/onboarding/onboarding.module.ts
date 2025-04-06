import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { OnboardingComponent } from './onboarding.component';
import { WelcomeComponent } from './components/welcome/welcome.component';
import { WizardComponent } from './components/wizard/wizard.component';
import { OnboardingService } from './onboarding.service';
import { WebSocketService } from './services/websocket.service';

const routes: Routes = [
  {
    path: '',
    component: OnboardingComponent,
    children: [
      { path: '', component: WelcomeComponent },
      { path: 'wizard', component: WizardComponent }
    ]
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    RouterModule.forChild(routes),
    OnboardingComponent,
    WelcomeComponent,
    WizardComponent
  ],
  providers: [
    OnboardingService,
    WebSocketService
  ],
  exports: [RouterModule]
})
export class OnboardingModule { }
