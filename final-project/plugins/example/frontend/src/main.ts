import { bootstrapApplication } from '@angular/platform-browser';
import { HelloComponent } from './app/hello.component';

bootstrapApplication(HelloComponent).catch(err => console.error(err));
