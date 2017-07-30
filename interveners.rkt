#lang racket

(require net/url)
(require racket/format)

(define (page_specific_url page_index)
  (string->url (string-append "https://scc-csc.lexum.com/scc-csc/scc-csc/en/2016/nav_neu.do?page=" (~a page_index) "&iframe=true")))

(define (get_docket_numbers case_url_tail)
  (sleep (/ (random 10 20) 10))
  (let ([page_content (port->string (get-pure-port (string->url (string-append "https://scc-csc.lexum.com/" case_url_tail "?iframe=true"))))])
    (regexp-match* #px"[0-9]{5}" (car (regexp-match #rx"Docket.*?</p>" page_content)))
    )
  )

(define (get_info cii_url)
  (sleep (/ (random 10 20) 10))
  (let ([page_content (port->string (get-pure-port cii_url))])
    (map
     (lambda (line) (get_docket_numbers (substring (car (regexp-match #rx"\"/.*?.do" line)) 1)))
     (regexp-match* #rx"<span class=\"title\">.*?</span>" page_content)
     )
    )
  )

(define get_docket_list
  (flatten
   (map
    (lambda (ind) (get_info (page_specific_url ind)))
    (stream->list (in-range 1 4))))
  )

(define (get_party_info docket_no)
  (sleep (/ (random 10 20) 10))
  (let ([page_content (port->string (get-pure-port (string->url (string-append "http://www.scc-csc.ca/case-dossier/info/parties-eng.aspx?cas=" docket_no))))])
    (regexp-match* #px"<td>[^\n]*</td>\\s*<td>Intervener</td>" page_content)
      )
  )

(map
(lambda (docket_no) (cons docket_no (get_party_info docket_no)))
 get_docket_list)