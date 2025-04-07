import { Component, OnDestroy, OnInit, ViewEncapsulation } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, interval, of, Subscription, switchMap, takeWhile } from 'rxjs';

interface TopicResponse {
  job_id: string;
}

interface Translation {
  english: string;
  japanese: string;
}

interface VocabularyItem {
  word: string;
  reading: string;
  romaji: string;
  meaning: string;
}

interface TopicResult {
  status: string;
  result?: {
    translation: Translation;
    vocabulary: VocabularyItem[];
  };
}

@Component({
  selector: 'plugin-wkcrawler',
  standalone: false,
  encapsulation: ViewEncapsulation.None,
  template: `
    <div class="plugin-wkcrawler">
      <div class="wkcrawler-input">
        <h2>Japanese Topic Explorer</h2>
        <div class="input-group">
          <input 
            type="text" 
            [(ngModel)]="topicText" 
            placeholder="Enter a topic in English"
            [disabled]="isProcessing">
          <button 
            (click)="submitTopic()" 
            [disabled]="!topicText || isProcessing">
            Explore
          </button>
        </div>
      </div>

      <div *ngIf="isProcessing" class="wkcrawler-loading">
        Processing topic...
      </div>

      <div *ngIf="isComplete" class="wkcrawler-result">
        <div class="translation-section">
          <h3>Translation</h3>
          <div class="translation">
            <p><strong>English:</strong> {{getTranslation().english}}</p>
            <p><strong>Japanese:</strong> {{getTranslation().japanese}}</p>
          </div>
        </div>

        <div class="vocabulary-section">
          <h3>Vocabulary</h3>
          <div class="vocabulary-list">
            <div *ngFor="let word of getVocabulary()" class="vocab-item">
              <div class="word">{{word.word}}</div>
              <div class="reading">{{word.reading}}</div>
              <div class="romaji">{{word.romaji}}</div>
              <div class="meaning">{{word.meaning}}</div>
            </div>
          </div>
          <div *ngIf="!hasVocabulary()" class="no-vocab">
            No vocabulary items found.
          </div>
        </div>
      </div>

      <div *ngIf="error" class="wkcrawler-error">
        {{error}}
      </div>
    </div>
  `
})
export class WkCrawlerComponent implements OnInit, OnDestroy {
  topicText = '';
  isProcessing = false;
  result: TopicResult | null = null;
  error: string | null = null;
  private pollSubscription?: Subscription;

  constructor(private http: HttpClient) {
    console.log('WkCrawlerComponent: Constructor');
  }

  ngOnInit(): void {
    console.log('WkCrawlerComponent: OnInit');
  }

  ngOnDestroy(): void {
    console.log('WkCrawlerComponent: OnDestroy');
    this.pollSubscription?.unsubscribe();
  }

  get isComplete(): boolean {
    return this.result?.status === 'complete' && !!this.result?.result;
  }

  getTranslation(): Translation {
    return this.result?.result?.translation || {
      english: 'Not available',
      japanese: 'Not available'
    };
  }

  getVocabulary(): VocabularyItem[] {
    return this.result?.result?.vocabulary || [];
  }

  hasVocabulary(): boolean {
    return (this.result?.result?.vocabulary?.length || 0) > 0;
  }

  async submitTopic() {
    if (!this.topicText || this.isProcessing) return;

    this.isProcessing = true;
    this.result = null;
    this.error = null;

    try {
      const response = await this.http.post<TopicResponse>(
        'http://localhost:8001/v1/topic',
        { english_text: this.topicText }
      ).toPromise();

      if (response?.job_id) {
        this.pollJobStatus(response.job_id);
      } else {
        throw new Error('No job ID received');
      }
    } catch (err) {
      this.error = 'Failed to submit topic';
      this.isProcessing = false;
    }
  }

  private pollJobStatus(jobId: string) {
    this.pollSubscription?.unsubscribe();
    
    this.pollSubscription = interval(1000)
      .pipe(
        switchMap(() => this.http.get<TopicResult>(`http://localhost:8001/v1/topic/${jobId}`)
          .pipe(catchError(() => of({ status: 'error', error: 'Failed to fetch status' })))
        ),
        takeWhile(response => response.status === 'processing', true)
      )
      .subscribe({
        next: (response) => {
          if (response.status === 'complete') {
            this.result = response;
            this.isProcessing = false;
          } else if (response.status === 'error') {
            this.error = 'Failed to process topic';
            this.isProcessing = false;
          }
        },
        error: () => {
          this.error = 'Failed to check status';
          this.isProcessing = false;
        }
      });
  }
}
