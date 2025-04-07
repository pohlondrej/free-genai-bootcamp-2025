import { Component, OnDestroy, OnInit, ViewEncapsulation } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, interval, of, Subscription, switchMap, takeWhile } from 'rxjs';

interface TopicResponse {
  job_id: string;
}

interface Article {
  title: string;
  english: string;
  japanese: string;
}

interface VocabularyItem {
  word: string;
  reading: string;
  romaji: string;
  meaning: string;
  isFavorited?: boolean;
}

interface TopicResult {
  status: string;
  result?: {
    article: Article;
    vocabulary: VocabularyItem[];
  };
}

@Component({
  selector: 'plugin-wkcrawler',
  standalone: false,
  encapsulation: ViewEncapsulation.None,
  styleUrls: ['./wkcrawler.component.scss'],
  template: `
    <div class="plugin-wkcrawler">
      <div class="page-header">
        <h1>Japanese Topic Explorer</h1>
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

      <div *ngIf="isProcessing" class="loading">
        Processing topic...
      </div>

      <div *ngIf="isComplete" class="result-section">
        <div class="article-card">
          <h2>{{getArticle().title}}</h2>
          <div class="translation">
            <div class="translation-item">
              <span class="label">English</span>
              <p>{{getArticle().english}}</p>
            </div>
            <div class="translation-item">
              <span class="label">Japanese</span>
              <p>{{getArticle().japanese}}</p>
            </div>
          </div>
        </div>

        <div class="vocabulary-section">
          <h2>Vocabulary</h2>
          <table class="vocabulary-table" *ngIf="hasVocabulary()">
            <thead>
              <tr>
                <th>Word</th>
                <th>Reading</th>
                <th>Romaji</th>
                <th>Meaning</th>
                <th>Favorite</th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let word of getVocabulary()">
                <td>{{word.word}}</td>
                <td>{{word.reading}}</td>
                <td>{{word.romaji}}</td>
                <td>{{word.meaning}}</td>
                <td>
                  <button 
                    class="favorite-btn" 
                    [class.favorited]="word.isFavorited"
                    [disabled]="word.isFavorited"
                    (click)="addToFavorites(word)"
                    [attr.title]="word.isFavorited ? 'Added to favorites!' : 'Add to favorites'">
                    <span class="heart-icon">♥</span>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          <div *ngIf="!hasVocabulary()" class="no-vocab">
            No vocabulary items found.
          </div>
        </div>
      </div>

      <div *ngIf="error" class="error">
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

  getArticle(): Article {
    return this.result?.result?.article || {
      title: 'Not available',
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

  async addToFavorites(word: VocabularyItem) {
    try {
      await this.http.post('/api/favorite', {
        word: word.word,
        reading: word.reading,
        romaji: word.romaji,
        meaning: word.meaning
      }).toPromise();
      
      word.isFavorited = true;
    } catch (err) {
      this.error = 'Failed to add word to favorites';
      setTimeout(() => this.error = null, 3000);
    }
  }
}
