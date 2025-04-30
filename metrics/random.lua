local counter = 1
local threads = {}

--setup ids for each thread
function setup(thread)
   thread:set("id", counter)
   table.insert(threads, thread)
   counter = counter + 1
end

--init variables for each thread
init = function(args)
   requests = 0
   responses = 0
   
   -- Variables to count responses
   counter_2xx = 0
   counter_4xx = 0
   counter_5xx = 0
   
   cache_hits = 0
   nginx_cache_hits = 0
   redis_cache_hits = 0

   local msg = "thread %d created"
   print(msg:format(id))
   math.randomseed(os.time() + id)
end

--make random requests
request = function()
   requests = requests + 1
   
   local reqid = math.random(1,20000)
   local path = "/user/"..reqid
   --print("id "..reqid)
   return wrk.format("GET", path)
end

--parse response
response = function(status, headers, body)
    responses = responses + 1

    if status >= 200 and status < 300 then
        counter_2xx = counter_2xx + 1
    elseif status >= 400 and status < 500 then
        counter_4xx = counter_4xx + 1
    elseif status >= 500 and status < 600 then
        counter_5xx = counter_5xx + 1
    end
    
    local nginx_cache_status = headers["X-Cache-Status"]
    local redis_cache_status = headers["X-App-Cache-Status"] --TBD: update with correct header
    
    --print(nginx_cache_status)
    --print(redis_cache_status)
    
    if nginx_cache_status then
       if string.match(tostring(nginx_cache_status), "HIT") then
           --print("!! nginx HIT")
           cache_hits = cache_hits + 1
           nginx_cache_hits = nginx_cache_hits + 1
       end
    elseif redis_cache_status then
        if string.match(tostring(redis_cache_status), "HIT") then
           cache_hits = cache_hits + 1
           redis_cache_hits = redis_cache_hits + 1
       end   
    end
end

--print stats at the end
done = function(summary, latency, requests)
   for index, thread in ipairs(threads) do
      local id        = thread:get("id")
      local requests  = thread:get("requests")
      local responses = thread:get("responses")
      local counter_2xx = thread:get("counter_2xx")
      local counter_4xx = thread:get("counter_4xx")
      local counter_5xx = thread:get("counter_5xx")
      local cache_hits = thread:get("cache_hits")
      local nginx_cache_hits = thread:get("nginx_cache_hits")
      local redis_cache_hits = thread:get("redis_cache_hits")

      local msg = "thread %d made %d requests and got %d responses; 2xx: %d, 4xx: %d, 5xx %d\ncache hits: %d, nginx: %d, redis: %d"
      print(msg:format(id, requests, responses, counter_2xx, counter_4xx, counter_5xx, cache_hits, nginx_cache_hits, redis_cache_hits))      
   end
end