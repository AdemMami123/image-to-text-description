var app = angular.module('imageApp', []);

app.controller('MainController', ['$scope', '$http', function($scope, $http) {
    $scope.description = "";
    $scope.image = null;

    $scope.generateDescription = function() {
        if (!$scope.image) {
            alert('Please select an image file.');
            return;
        }

        var formData = new FormData();
        formData.append('file', $scope.image);
        formData.append('prompt', $scope.description);

        $http.post('/predict', formData, {
            transformRequest: angular.identity,
            headers: { 'Content-Type': undefined }
        }).then(function(response) {
            $scope.description = response.data.description;
        }).catch(function(error) {
            console.error('Error:', error);
            $scope.description = "Error generating description.";
        });
    };

    $scope.fileChanged = function(element) {
        $scope.$apply(function(scope) {
            var file = element.files[0];
            $scope.image = file;
        });
    };

}]);

app.directive('fileInput', ['$parse', function($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            element.on('change', function(event) {
                var files = event.target.files;
                $parse(attrs.fileInput).assign(scope, element[0].files[0]);
                scope.fileChanged(element[0]);
                scope.$apply();
            });
        }
    };
}]);
