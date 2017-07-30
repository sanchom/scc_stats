#lang racket

(require net/url)
(require racket/format)

(define (page_specific_url page_index)
  (string->url (string-append "https://scc-csc.lexum.com/scc-csc/scc-csc/en/2016/nav_neu.do?page=" (~a page_index) "&iframe=true")))

(define (get_case_info case_url_tail)
  (let ([page_content (port->string (get-pure-port (string->url (string-append "https://scc-csc.lexum.com/" case_url_tail "?iframe=true"))))])
    (regexp-match* #px"[0-9]{5}" (car (regexp-match #rx"Docket.*?</p>" page_content)))
    )
  )

(define (get_info cii_url)
  (let ([page_content (port->string (get-pure-port cii_url))])
    (map
     (lambda (line) (get_case_info (substring (car (regexp-match #rx"\"/.*?.do" line)) 1)))
     (regexp-match* #rx"<span class=\"title\">.*?</span>" page_content)
     )
    )
  )

(flatten
 (map
  (lambda (ind) (get_info (page_specific_url ind)))
  (stream->list (in-range 1 4))))