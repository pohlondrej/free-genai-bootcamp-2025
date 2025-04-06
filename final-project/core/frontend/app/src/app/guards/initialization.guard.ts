import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { map, catchError, tap } from 'rxjs/operators';
import { of } from 'rxjs';
import { OnboardingService, OnboardingStatus } from '../onboarding/onboarding.service';

export const initializationGuard = () => {
  const router = inject(Router);
  const onboardingService = inject(OnboardingService);

  return onboardingService.getStatus().pipe(
    tap(status => console.log('Initialization status:', status)),
    map((status: OnboardingStatus) => {
      if (!status.is_initialized) {
        console.log('App not initialized, redirecting to onboarding');
        router.navigate(['/onboarding']);
        return false;
      }
      console.log('App is initialized, allowing navigation');
      return true;
    }),
    catchError((error) => {
      console.error('Error checking initialization status:', error);
      router.navigate(['/onboarding']);
      return of(false);
    })
  );
};
