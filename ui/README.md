## UI学习总结
###  使用的框架和技术
  * jquery
  * bootstrap
  * angular
  * angular-ui-bootstrap
###  详细说明
  1. bootstrap大屏幕
    
        首页使用大屏幕 突出主题，使用bootstrap css jumbotron

  2. bootstrap折叠框
  
        大屏幕中添加按钮 实现折叠框的功能。collapse

  3. bootstrap 表单
        
        bootstrap css form-horizontal form-group col-sm-10 form-control
        这些bootstrap样式 可以使表单看起来更美观。表单中的每个input
        还可以合angular的ng-model结合，将值和模型绑定。
        e.g ng-model="object.title" 表单提交的按钮可以和ng-click绑定处理方法，
        e.g ng-click="confirm()" 然后在script中实现confirm()方法。
  4. bootstrap 输入框组
  
        input-group input-group-addon 

  5. angular list
        自动生成list内容 可以使用angular 的 ng-repeat，
        可以实现list的过滤，排序以及协助分页，e.g. ng-repeat="urlinfo in
        urlinfos | filter:query |
        orderBy:['-vote']|paging:page.index:page.size" （-加断线是倒序） 

  6. angular 模态框
        
        angular modal, angular-ui-bootstrap提供的关于模态框的实现可以使用 
        ```javascript
        var info_app = angular.module('infos', ['ui.bootstrap']);
        info_app.controller('infoCtrl', function($scope, $http, $log, $uibModal) {
            $scope.update = function(size, urlinfo) {
            	$scope.urlinfo = urlinfo;
                var modalInstance = $uibModal.open({
                	templateUrl: 'myModalContent.html',
                	controller: 'modalInstanceCtrl',
                	size: size,
                	resolve: {
                        urlinfo : function(){return $scope.urlinfo}
                    }
                	
                });

                modalInstance.opened.then(function(){
                	//function to exec after modal window opened
                	console.log('modal is opened');
                });

                modalInstance.result.then(function(result){
                	console.log(result);
                }, function(reason){
                	//点击空白区，总会输出backdrop click,点击取消 则会输出cancel
                    console.log(reason);
                    $log.info('Modal dismissed at: ' + new Date());
                });
            };
        });
        
        info_app.controller('modalInstanceCtrl', function ($scope, $http, $uibModalInstance, urlinfo) {
            $scope.urlinfo = urlinfo;
            $scope.ok = function (urlinfo) {
                $http({
                    method  : 'PUT',
                    url     : 'http://10.62.57.242:5000/urls/' + $scope.urlinfo.key,
                    data    : $scope.urlinfo,                    
                    headers : {'Content-Type': 'application/json'}
                })
                .success(function(data) {
                })
                .error(function(data) {
                	console.log(data);
                });

                $uibModalInstance.dismiss('cancel');
            };

            $scope.cancel = function () {
                $uibModalInstance.dismiss('cancel');
           };

        });
        ```    
  7. angular 分页
        angular uib-pagination 有对分页的默认实现
        ```html
        <ul uib-pagination  total-items="urlinfos | filter:query | size" ng-model="page.index" max-size="5"
            items-per-page="page.size"
            class="pagination-sm pull-right" boundary-links="true">
        </ul>
        ```
        还需要结合自定义的filter实现分页功能：
        ```javascript
        info_app.filter('paging', function() {
            var pageSize = 5;
            return function (urlinfos, index, pageSize) {
                if (!urlinfos)
                    return [];

                var offset = (index - 1) * pageSize;
                return urlinfos.slice(offset, offset + pageSize);
            }
        });

        
        info_app.filter('size', function() {
            return function (urlinfos) {
                if (!urlinfos)
                    return 0;

                return urlinfos.length || 0
            }
        });
        ```
        


  
