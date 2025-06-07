;; List contents of ~/.todo.txt

(require ['clojure.string :as 'str])

(defn expand-user [path]
  (clojure.string/replace-first path "~" (System/getProperty "user.home")))

(def todo-path (expand-user "~/.todo.txt"))
(def lines (str/split-lines (slurp todo-path)))

(def line-number 1)
(doseq [line lines]
  (println "Task" line-number "-" line)
  (def line-number (inc line-number)))

