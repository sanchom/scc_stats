#lang racket

(require net/url)
(require racket/format)

(define (build-paged-url year page-index)
  (string->url (string-append "https://scc-csc.lexum.com/scc-csc/scc-csc/en/" year "/nav_neu.do?page=" (~a page-index) "&iframe=true")))

(define (build-judgement-url judgement-slug)
  (string->url (string-append "https://scc-csc.lexum.com/" judgement-slug "?iframe=true")))

(define (build-docket-info-url docket-no)
  (string->url (string-append "https://www.scc-csc.ca/case-dossier/info/parties-eng.aspx?cas=" docket-no)))

(define (get-docket-numbers-from-judgement judgement-slug)
  (sleep (/ (random 20 30) 10))
  (let ([page-content (port->string (get-pure-port (build-judgement-url judgement-slug)))])
    (regexp-match* #px"[0-9]{5}" (car (regexp-match #rx"Docket.*?</p>" page-content)))))

(define (get-list-of-judgements cii-index-url)
  (sleep (/ (random 20 30) 10))
  (let ([page-content (port->string (get-pure-port cii-index-url))])
    (map
     (lambda (line) (get-docket-numbers-from-judgement (substring (car (regexp-match #rx"\"/.*?.do" line)) 1)))
     (regexp-match* #rx"<span class=\"title\">.*?</span>" page-content))))

(define (get-docket-list year)
  (flatten
   (map
    (lambda (ind) (get-list-of-judgements (build-paged-url year ind)))
    (stream->list (in-range 1 5)))))

(define (get-fake-party-content docket-no)
  (port->string (open-input-file "fake_docket_source.html" #:mode 'text)))

(define (get-real-party-content docket-no)
  (port->string (get-pure-port (build-docket-info-url docket-no))))

(define (get-party-content docket-no) (get-real-party-content docket-no))

(define (extract-interveners unparsed-intervener-list)
  (map (lambda (unparsed-line) (car (cdr (regexp-match #rx"<td>(.*?)</td>" unparsed-line))))
       unparsed-intervener-list))

(define (get-docket-info docket-no)
  (sleep (/ (random 20 30) 10))
  (let ([page-content (get-party-content docket-no)])
    (define as-of-right (string-contains? page-content "(As of Right)"))
    (define intervener-list (extract-interveners (regexp-match* #px"<td>[^\n]*</td>\\s*<td>Intervener</td>" page-content)))
    (define case-name (car (cdr (regexp-match #rx"<p class=\"font-large\"><b>(.*?)</b>" page-content))))
    (cons docket-no (cons case-name (cons as-of-right intervener-list)))))

(define (write-docket-info year docket-info)
  (define docket-no (car docket-info))
  (define as-of-right (cadr docket-info))
  (define case-name (caddr docket-info))
  (define interveners (cdddr docket-info))
  (if (empty? interveners)
      (printf "~a\t~a\t~a\t~a\n" year docket-no case-name as-of-right)
      (for-each (lambda (intervener) (printf "~a\t~a\t~a\t~a\t~a\n" year docket-no case-name as-of-right intervener))
                interveners)))

(define (write-info-for-year year)
  (for-each (lambda (docket-no) (write-docket-info year (get-docket-info docket-no))) (get-docket-list year)))

(for-each (lambda (year) (write-info-for-year year)) '("2017"))