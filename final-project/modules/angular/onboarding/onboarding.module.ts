import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OnboardingComponent } from './onboarding.component';
import { WelcomeComponent } from './components/welcome/welcome.component';
import { WizardComponent } from './components/wizard/wizard.component';

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
    RouterModule.forChild(routes),
    OnboardingComponent,
    WelcomeComponent,
    WizardComponent
  ],
  exports: [RouterModule]
})
export class OnboardingModule { }
